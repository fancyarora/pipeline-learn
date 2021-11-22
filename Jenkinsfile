pipeline {
    agent none
    stages {
         stage('Build') {
             agent { 
                 docker {
                     image 'python:3.8-slim-buster'
                 }
             }
             steps {
                 sh 'python -m py_compile sources/prism.py'

                 stash(name: 'compiled-results', includes: 'sources/*.py*')
             }
         }
         stage('test') {
             agent {
                 docker {
                     image 'python:3.8-slim-buster'
                     args '-u root'
                 }
             }
             steps {
                 sh 'apt-get install -y libpq5'

                 sh 'pip install -r requirements.txt'

                 sh 'python sources/tests.py'
             }
             post{
                 always{
                     junit 'test-reports/*.xml'
                 }
             }
         }
    }
}