# ImageCompressionLambda

A Python 3 Lambda script which utilizes Pillow for aggressive PNG image compression. It uses Pillow and Python 3.6.1 to achieve the following:

* Currently supports PNG, with other images potentially working with modification
* Changes the image mode to `P (8-bit pixels, mapped to any other mode using a color palette)`
* Modifies palette to Web
* Sets highest level ZLIB compression
* Utilizes the optimized pillow PNG writer

This is all done in memory, but can still do pretty well with 2.2MB or so images on a 128MB Lambda. If you need to go larger than that increase the Lambda memory size. For best isolation it's recommended to have the Lambda in a VPC with an S3 endpoint. Note that unless that VPC has a NAT Gateway it won't be able to reach out to any other non-VPC ready AWS services, or external sites in general.

## Requirements

To make things as simple as possible a ZIP of the current version of the lambda is included. It's been built using an EC2 instance based off of the Lambda supported environment and customized using an [SSM Automation DOcument](https://gist.github.com/cwgem/b898cf04fa65dc1763a374170ab1d42c). Outside of that you'll need:

* An S3 event setup to trigger based on images
* A Lambda function that has Execution roles as well as GetObject and PutObject S3 permissions
* The Lambda function utilizes environment variables to setup the basic conversion. These include:
  * OUTPUT_IMAGE_PATH -> The output path in S3 to store the resulting image
  * IMAGE_MODE -> The image mode to convert to. Default is `P (8-bit pixels, mapped to any other mode using a color palette)`
  * IMAGE_PALETTE -> The palette to use for conversion. Default is `WEB`

## Usage

Simply setup the Lambda to trigger on an appropriate PUT event. It will compress according to settings and output to the given output path.

## Updating

Since the supporting libraries are already there simply updating the zip file with the new code should suffice. If you need to use other python modules you're going to have to rebuild it from an EC2 instance. See Requirements for an SSM doc that will get you one up and running fairly easy.

## Support

This repository is primarily meant for educational purposes. If you want to customize it you're better off forking. Pull requests will only be taken if they are specific to PNG and enable far better compression, or reduce overall Lambda execution time.
