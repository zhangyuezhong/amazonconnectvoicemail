set AWS_PROFILE=purple

set s3-bucket=amazon-connect-d747e77f7d22
set s3-prefix=deploy_artifacts
set stack-name=ac-lex-bootstrapper


set parameter-override=
set parameter-override=%parameter-override% Prefix=dev

set tags=
set tags=%tags% Owner="Your Name"
set tags=%tags% Purpose="Amazon Template"

set template-file=cloudformation/template.yaml
set output-template-file=cloudformation/template.json

aws cloudformation package --template-file %template-file% --s3-bucket %s3-bucket% --s3-prefix %s3-prefix% --output-template-file %output-template-file% --use-json
aws cloudformation deploy --template-file %output-template-file% --stack-name %stack-name% --s3-bucket %s3-bucket% --s3-prefix %s3-prefix%  --parameter-override %parameter-override% --tags %tags% --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND

