provider "aws" {
  region     = "us-east-1"
  access_key = "AWS_ACCESS_KEY_HARDCODED"
  secret_key = "AWS_SECRET_KEY_HARDCODED"
}

provider "azurerm" {
  features {}
  subscription_id = "AZURE_SUBSCRIPTION_ID_HARDCODED"
  client_id       = "AZURE_CLIENT_ID_HARDCODED"
  client_secret   = "AZURE_CLIENT_SECRET_HARDCODED"
  tenant_id       = "AZURE_TENANT_ID_HARDCODED"
}

resource "aws_instance" "frontend" {
  ami           = "ami-0c55b159cbfafe1f0" # Example AMI
  instance_type = "t2.micro"

  tags = {
    Name = "Frontend-Server"
  }
}

resource "azurerm_virtual_machine" "backend" {
  name                  = "Backend-VM"
  location              = "East US"
  resource_group_name   = azurerm_resource_group.rg.name
  network_interface_ids = [azurerm_network_interface.backend_nic.id]
  vm_size               = "Standard_B1s"

  os_profile = {
    computer_name  = "backendvm"
    admin_username = "adminuser"
    admin_password = "AdminPassword123!" # Hardcoded credentials for testing
  }

  os_profile_linux_config {
    disable_password_authentication = false
  }

  storage_os_disk = {
    name              = "backend-osdisk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}

resource "aws_db_instance" "database" {
  allocated_storage    = 20
  engine               = "mysql"
  instance_class       = "db.t2.micro"
  name                 = "mydb"
  username             = "dbadmin"
  password             = "DBAdminPassword123!" # Hardcoded credentials for testing
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
}
