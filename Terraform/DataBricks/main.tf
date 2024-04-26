provider "azurerm" {
  features {}
}
provider "azuredevops" {
  org_service_url       = "https://dev.azure.com/bayareala8s"
  personal_access_token = var.personal_access_token
}

variable "personal_access_token" {
  description = "The Personal Access Token for Azure DevOps"
  sensitive   = true
}

variable "databricks_token" {}

provider "databricks" {

  host  = azurerm_databricks_workspace.main.workspace_url
  token = var.databricks_token
}

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~>0.3"
    }
    azuredevops = {
      source  = "microsoft/azuredevops"
      version = "~>0.1.4"
    }
  }
}

resource "azurerm_resource_group" "main" {
  name     = "cdp-app-dev-westus-databricks-rg"
  location = "westus2"
}

resource "azurerm_databricks_workspace" "main" {
  name                        = "cdp-app-dev-westus-databricks-ws"
  resource_group_name         = azurerm_resource_group.main.name
  location                    = azurerm_resource_group.main.location
  sku                         = "standard"
  managed_resource_group_name = "${azurerm_resource_group.main.name}-managed"
}

resource "azurerm_storage_account" "main" {
  name                     = "cdpappdevstorage"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "RAGRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = true
}

resource "azurerm_storage_data_lake_gen2_filesystem" "main" {
  name               = "cdp-app-dev-filesystem"
  storage_account_id = azurerm_storage_account.main.id
}

resource "azuredevops_project" "project" {
  name               = "cdp-app-dev-databricks-project"
  visibility         = "private"
  version_control    = "Git"
  work_item_template = "Agile"
}

resource "azuredevops_build_definition" "build_definition" {
  project_id = azuredevops_project.project.id
  name       = "cdp-app-dev-databricks-build-definition"

  ci_trigger {
    use_yaml = true
  }

  repository {
    repo_type   = "TfsGit"
    repo_id     = azuredevops_git_repository.repository.id
    branch_name = azuredevops_git_repository.repository.default_branch
    yml_path    = "azure-pipelines.yml"
  }
}

resource "azuredevops_git_repository" "repository" {
  project_id = azuredevops_project.project.id
  name       = "cdp-app-dev-databricks-repository"
  initialization {
    init_type = "Clean"
  }
}

resource "time_sleep" "wait" {
  depends_on = [azurerm_databricks_workspace.main]

  create_duration = "5m"
}

resource "databricks_cluster" "main" {
  cluster_name            = "cdp_app_dev_databrick_cluster"
  spark_version           = "14.3.x-scala2.12"
  node_type_id            = "Standard_D3_v2"
  autotermination_minutes = 20

  autoscale {
    min_workers = 1
    max_workers = 2
  }
  depends_on = [time_sleep.wait]
}