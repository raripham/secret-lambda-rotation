# secret-lambda-rotation

## Create lambda with image
![image](https://user-images.githubusercontent.com/94727826/197728076-2ceba139-d0a9-47c4-b161-9c722eb80431.png)

## Configure
### + Permission
      SecretsManagerAccess
   ![image](https://user-images.githubusercontent.com/94727826/197728785-aa25ee7c-097a-4015-b336-052f8ec7ae87.png)
### + VPC
      select subnet private with natgateway to can call API of secret manager
   ![image](https://user-images.githubusercontent.com/94727826/197729676-0a853c2d-02b5-4f2d-b6b1-acc60e17cbf1.png)
### + EndPoint lambda (subnet private added above)
   ![image](https://user-images.githubusercontent.com/94727826/197730105-ffb61c2e-1d7e-45cc-8c1d-dedbf0e09545.png)

