output "resource_group_name" {
  value       = azurerm_resource_group.rg.name
  description = "Name of the resource group"
}

output "acr_login_server" {
  value       = azurerm_container_registry.acr.login_server
  description = "ACR login server (use in your image tag)"
}

output "aks_name" {
  value       = azurerm_kubernetes_cluster.aks.name
  description = "AKS cluster name"
}

output "aks_resource_group" {
  value       = azurerm_resource_group.rg.name
  description = "Resource group containing the AKS cluster"
}
