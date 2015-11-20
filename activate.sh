nvm install 4
nvm use 4
npm install
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements.dev.txt
if [ ! -f .git/hooks/pre-commit ]; then
    echo -e "#!/bin/sh\n\n\nnpm run check" > .git/hooks/pre-commit
fi
