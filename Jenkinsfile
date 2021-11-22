pipeline {
    agent none
    stages {
         stage('Build') {
             agent { 
                 docker {
                     image 'python:3.8-slim-buster'
                     args '-u root'
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
                 sh 'pip install -r requirements.txt'

                 sh 'python sources/tests.py'
             }
             post{
                 always{
                     junit 'test-reports/*.xml'
                 }
             }
         }
         stage('Deploy'){
             agent any
             environment{
                 VOLUME = '$(pwd)/sources:/src'
                 IMAGE = 'cdrx/pyinstaller-linux:python3'
             }
             steps{
                 dir(path: env.BUILD_ID) {
                     unstash(name: 'compiled-results')
                     sh "docker run --rm -v ${VOLUME} ${IMAGE} 'pyinstaller -F prism.py'"
                 }

                sh "docker run -d -p 5000:5000 --restart=always --name registry registry:2"

                sh "docker build -t localhost:5000/prism ."

                sh "docker push localhost:5000/prism"
             }
             post{
                 success{
                     archiveArtifacts "${env.BUILD_ID}/sources/dist/prism"

                     sh "kubectl create --filename deployment.yaml"

                     sh "minikube image load localhost:5000/prism:latest"
                 }
             }
         }
    }
}