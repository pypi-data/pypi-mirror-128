WAIT_TIME = 1

READY_SESSION_STATUS = "READY"
PROVISIONING_SESSION_STATUS = "PROVISIONING"
NOT_FOUND_SESSION_STATUS = "NOT_FOUND"
FAILED_SESSION_STATUS = "FAILED"
UNHEALTHY_SESSION_STATUS = [NOT_FOUND_SESSION_STATUS, FAILED_SESSION_STATUS]

ERROR_STATEMENT_STATUS = "ERROR"
CANCELLED_STATEMENT_STATUS = "CANCELLED"
AVAILABLE_STATEMENT_STATUS = "AVAILABLE"
FINAL_STATEMENT_STATUS = [ERROR_STATEMENT_STATUS, CANCELLED_STATEMENT_STATUS, AVAILABLE_STATEMENT_STATUS]
SQL_CELL_MAGIC = "%%sql"

CELL_MAGICS = {"%%configure", "%%sql"}

HELP_TEXT = f'''
Available Magic Commands

## Sessions Magics
%help | Return a list of descriptions and input types for all magic commands. 
%profile | String | Specify a profile in your aws configuration to use as the credentials provider.
%region | String | Specify the AWS region in which to initialize a session | Default from ~/.aws/configure
%idle_timeout | Int | The number of minutes of inactivity after which a session will timeout. The default idle timeout value is 2880 minutes.
%session_id | Returns the session ID for the running session. 
%status | Returns the status of the current Glue session including its duration, configuration and executing user / role.
%list_sessions | Lists all currently running sessions by name and ID.

## Glue Config Magics
%%configure | Dictionary | A json-formatted dictionary consisting of all configuration parameters for a session. Each parameter can be specified here or through individual magics.
%glue_role_arn | String | Specify an IAM role ARN to execute your session with. | Default from ~/.aws/configure
%number_of_workers | int | The number of workers of a defined worker_type that are allocated when a job runs. worker_type must be set too.
%worker_type | String | Standard, G.1X, or G.2X. number_of_workers must be set too. 
%security_config | String | Define a Security Configuration to be used with this session. 
%connections | List | Specify a comma separated list of connections to use in the session.
%additional_python_modules | List | Comma separated list of additional Python modules to include in your cluster (can be from Pypi or S3).
%extra_py_files | List | Comma separated list of additional Python files From S3.
%extra_jars | List | Comma separated list of additional Jars to include in the cluster.

## Action Magics
%%sql | String | Run SQL code. All lines after the initial %%sql magic will be passed as part of the SQL code. 
'''
