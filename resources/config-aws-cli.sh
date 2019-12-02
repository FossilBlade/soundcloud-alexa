echo "Configuring AWS with ECS User Credentials"
mkdir ~/.aws
echo "[profile lm]" >> ~/.aws/config
echo "output = json" >> ~/.aws/config
echo "region = ap-south-1" >>  ~/.aws/config

echo "[lm]" > ~/.aws/credentials
echo "aws_access_key_id = AKIAZYP2QYQF3D2G5AEW" >> ~/.aws/credentials
echo "aws_secret_access_key = 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" >>  ~/.aws/credentials