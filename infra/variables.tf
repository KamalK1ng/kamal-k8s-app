variable "location" {
  type        = string
  description = "Azure region"
  default     = "westeurope"
}

variable "rg_name" {
  type        = string
  description = "Resource group name"
  default     = "kamal-k8-rg"
}

variable "acr_name" {
  type        = string
  description = "Azure Container Registry name (must be globally unique, lowercase)"
  default     = "kamalk8acr"
}

variable "aks_name" {
  type        = string
  description = "AKS cluster name"
  default     = "kamal-k8s-aks"
}

variable "node_vm_size" {
  type        = string
  description = "VM size for AKS node pool"
  default     = "Standard_B2s"
}

variable "node_count" {
  type        = number
  description = "Number of nodes in default node pool"
  default     = 1
}
# kamalk8acr.azurecr.io