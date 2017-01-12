VENV_DIR = '.venv'


def vsh *args
  sh ". #{VENV_DIR}/bin/activate && #{args.join ' '}"
end


task :test do
  sh "python3 -m venv #{VENV_DIR}"
  vsh 'pip install mecab-python3'
  vsh 'python setup.py install'
  vsh 'nltokeniz data/foo.en'
  vsh 'nltokeniz -l english data/foo.en'
  vsh 'nltokeniz -l japanese data/foo.ja'
end


task :upload => :test do
    sh 'python3 setup.py sdist bdist_wheel'
    sh 'twine upload dist/*'
end


task :clean do
  sh 'git clean -dfx'
end
