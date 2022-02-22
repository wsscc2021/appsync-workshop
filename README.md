
### post API

게시글을 저장하고 읽어드리는 API를 구현합니다.

게시글은 Aurora Database의 post table에 저장합니다.

```
CREATE TABLE db.post (
  id VARCHAR(255) PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  content VARCHAR(255) NOT NULL,
  createdAt VARCHAR(255) NOT NULL,
  author VARCHAR(255) DEFAULT 'anonymous'
);
```

mutation

- createPost
  
  게시글을 1개 생성합니다.
  
  생성 시간은 사용자가 지정하는 것이 아니라, 자동으로 기록되도록 합니다.

query

- listPost
  
  최근 10개 게시글을 리스트로 읽어옵니다.

- getPost
  
  특정 ID를 가진 게시글을 읽어옵니다.

### comment API

댓글을 저장하고 읽어드리는 API를 구현합니다.

댓글은 DynamoDB comment table에 저장합니다.

```
postId - PK
commentId - SK
comment - Attribute
author - Attribute
createdAt - Attribute
```

mutation

- createContent
  
  게시글에 댓글을 1개 생성합니다.
  
  생성 시간은 사용자가 지정하는 것이 아니라, 자동으로 기록되도록 합니다.

query

- listComment
  
  게시글의 최근 10개 댓글을 읽어옵니다.

- getComment
  
  특정 ID를 가진 댓글을 읽어옵니다.



# Welcome to your CDK Python project!

This is a blank project for Python development with CDK.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
