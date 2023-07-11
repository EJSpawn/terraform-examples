#data fixa
variable "year" {
  description = "The year"
  type        = number
  default     = 2022
}

variable "month" {
  description = "The month"
  type        = number
  default     = 2
}

locals {
  first_day_next_month = timeadd(time_static(format("%04d-%02d-01T00:00:00Z", var.year, var.month + 1)), "0s")
  last_day_of_month    = timeadd(local.first_day_next_month, "-24h")
  formatted_date       = formatdate("YYYY-MM-DD", local.last_day_of_month)
}

#data atual
output "last_day_of_month" {
  value = local.formatted_date
}


locals {
  current_time  = timestamp()
  ten_days_ago  = timeadd(local.current_time, "-240h") # 10 dias são 240 horas
  formatted_date = formatdate("YYYY-MM-DD", local.ten_days_ago)
}

output "ten_days_ago" {
  value = local.formatted_date
}

#lista
variable "original_list" {
  description = "The original list"
  type        = list(string)
  default     = ["value1", "value2"]
}

locals {
  new_list = concat(var.original_list, ["value3", "value4"])
}

output "new_list" {
  value = local.new_list
}