### Steps to create Azure DataBricks Workspace & Cluster with Terraform

To create an Azure Databricks Workspace and Cluster with Terraform, you can follow these steps:

1. **Set up Terraform**: Ensure that you have Terraform installed on your machine. If not, you can install it using Homebrew as described in the previous conversation.

2. **Create a Terraform configuration file**: This file will contain the necessary resources to create the Azure Databricks Workspace and Cluster. 

Here is a sample Terraform configuration file (`main.tf`) for creating an Azure Databricks Workspace and Cluster:

```hcl
provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "example-resources"
  location = "West Europe"
}

resource "azurerm_databricks_workspace" "example" {
  name                        = "example-workspace"
  resource_group_name         = azurerm_resource_group.example.name
  location                    = azurerm_resource_group.example.location
  sku                         = "Standard"
  managed_resource_group_name = "example-managed-resources"
}

resource "azurerm_databricks_cluster" "example" {
  name                      = "example-cluster"
  resource_group_name       = azurerm_resource_group.example.name
  workspace_name            = azurerm_databricks_workspace.example.name
  num_workers               = 1
  spark_version             = "6.4.x-scala2.11"
  spark_conf                = {
    "spark.speculation" = "true"
  }
  custom_libs_conf          = {
    "whitelistedLibraries" = ["com.databricks:dbutils-api_2.11:0.0.4"]
  }
  node_type_id              = "Standard_D3_v2"
  autoscale {
    min_workers = 1
    max_workers = 2
  }
}
```

3. **Initialize Terraform**: Run `terraform init` in the directory containing your `main.tf` file. This will download the necessary provider plugins.

4. **Plan and apply the configuration**: Run `terraform plan` to see what changes will be made. Then run `terraform apply` to create the resources. You will be asked to confirm the changes.

Please replace the placeholders with your actual values. Also, ensure that you have the necessary permissions to create resources in Azure.


### Commands for DataBricks-cli


The Databricks CLI (Command Line Interface) provides an easy to use interface to the Databricks platform. Here are the main commands:

databricks configure [--token]: Configures the authentication credentials for the CLI.

databricks workspace ls [OPTIONS] [PATH]: Lists objects in the Databricks workspace.

databricks workspace rm [OPTIONS] PATH: Removes an object from the Databricks workspace.

databricks workspace import [OPTIONS] SOURCE_PATH TARGET_PATH: Imports a file to the Databricks workspace.

databricks workspace export [OPTIONS] SOURCE_PATH TARGET_PATH: Exports a file from the Databricks workspace.

databricks fs cp [OPTIONS] SRC DST: Copies files to and from DBFS.

databricks fs rm [OPTIONS] PATH: Removes files from DBFS.

databricks fs ls [OPTIONS] DIRECTORY: Lists files in DBFS.

databricks fs mkdirs PATH: Makes directories in DBFS.

databricks fs move [OPTIONS] SRC DST: Moves a file in DBFS.

databricks jobs list: Lists all jobs.

databricks jobs create --json JSON: Creates a new job.

databricks jobs delete --job-id JOB_ID: Deletes a job.

databricks jobs get --job-id JOB_ID: Retrieves the details of a job.

databricks jobs reset --json JSON: Resets the definition of a job.

databricks jobs run-now --job-id JOB_ID: Runs a job now.

databricks clusters list: Lists all clusters.

databricks clusters create --json JSON: Creates a new cluster.

databricks clusters delete --cluster-id CLUSTER_ID: Deletes a cluster.

databricks clusters get --cluster-id CLUSTER_ID: Retrieves the details of a cluster.

databricks clusters edit --json JSON: Edits the configuration of a cluster.

databricks clusters start --cluster-id CLUSTER_ID: Starts a cluster.

databricks clusters restart --cluster-id CLUSTER_ID: Restarts a cluster.

databricks clusters events --cluster-id CLUSTER_ID: Lists events for a cluster.

databricks secrets create-scope --scope SCOPE: Creates a new secret scope.

databricks secrets list-scopes: Lists all secret scopes.

databricks secrets delete-scope --scope SCOPE: Deletes a secret scope.

databricks secrets put --scope SCOPE --key KEY: Puts a secret in a scope.

databricks secrets delete --scope SCOPE --key KEY: Deletes a secret.

databricks secrets list --scope SCOPE: Lists all secrets in a scope.

databricks libraries install --cluster-id CLUSTER_ID --maven-coordinates GROUP_ID:ARTIFACT_ID:VERSION: Installs a Maven library on a cluster.

databricks libraries uninstall --cluster-id CLUSTER_ID --maven-coordinates GROUP_ID:ARTIFACT_ID:VERSION: Uninstalls a Maven library from a cluster.

databricks libraries list --cluster-id CLUSTER_ID: Lists all libraries installed on a cluster.

For more details on how to use these commands, you can use the --help option with any command, like databricks workspace ls --help.
