# pygeon

## install packages
    # yum groupinstall "Development tools"
    # yum install gcc zlib-devel bzip2 bzip2-devel readline readline-devel sqlite sqlite-devel openssl openssl-devel git GConf2

## pyenv
    $ git clone https://github.com/yyuu/pyenv.git ~/.pyenv
    $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    $ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    $ echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    $ source ~/.bashrc

## install python3.6.6
    $ pyenv install 3.6.6

## download selenium, chromedriver
    selenium-server-standalone-3.13.0.jar

## make vitrtualenv dir
    $ virtualenv foobardir

## into vitrtualenv
    $ cd foobardir
    $ pyenv local 3.6.6
    (foobardir) $ source bin/activate

## pip in virtualenv
    (foobardir) $ pip install -r FREEZE.txt

## STEP1
#### 市区町村データを取得
    (foobardir) $ python make_list.py MakeList.test_make_list

# STEP2
#### 5市区町村ずつページングしながら詳細リンクのhrefを取得（faxがある場合表示）
(foobardir) $ python make_list.py MakeList.test_scrape_detail_link

# STEP3
#### 業者の詳細ページを解析取得
(foobardir) $ python make_list.py MakeList.test_scrape_agent
