terraform {
  required_version = ">= 1.6.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.116"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "azurerm" {
  features {}
}

########################
# Resource Group
########################

resource "azurerm_resource_group" "rg" {
  name     = var.rg_name
  location = var.location
}

########################
# Azure Container Registry
########################

resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = false
}

########################
# AKS Cluster
########################

resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${var.aks_name}-dns"


  default_node_pool {
    name       = "system"
    vm_size    = var.node_vm_size
    node_count = var.node_count
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }

  role_based_access_control_enabled = true
}

########################
# Allow AKS to pull from ACR
########################

resource "azurerm_role_assignment" "aks_acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"

  # The identity used by the nodes to pull images
  principal_id = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
}
