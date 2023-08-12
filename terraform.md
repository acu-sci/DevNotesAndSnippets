# Terrraform Workflow

. Start Terraform in a folder with .tf files  
> terraform init  

. Get preview of resources to generate/adapt  
> terraform plan  

. Target the changes only to a given module  
> terraform plan -target {type}.{name}  

e.g.  

> terraform plan -target module.monitoring
> terraform apply