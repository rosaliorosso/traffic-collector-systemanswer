SystemAnswer�g���t�B�b�N�擾�c�[��
=========

�ړI
---------------

�{�c�[���́A�A�C�r�[�V�[������Ђ��񋟂���System Answer G2���g���t�B�b�N���������Ŏ擾���邽�߂̃c�[���ł�
Python�ɂ�SystemAnswer�Ɏ������O�C�����A�Ώۃg���t�B�b�N��PNG/CSV���_�E�����[�h���܂��B

���O����
---------------

�c�[�������s����O�ɉ��L�̐ݒ�t�@�C���ɕK�v�������L�����Ă�������

login.json  

| Left align | Right align |
|:-----------|:------------|
| baseurl    | �K�{�BSystemAnswer��URL |
| username   | �K�{�BSystemAnswer�̃��[�UID |
| userpass   | �K�{�BSystemAnswer�̃��[�U�p�X���[�h |

node.json

| Left align | Right align |
|:-----------|:------------|
| hostname     | �K�{�B�g���t�B�b�N�擾�Ώۂ̃z�X�g���B�t�@�C���ۑ����Ɏg�p |
| hostid       | �K�{�B�g���t�B�b�N�擾�Ώۂ̃z�X�gID�BSystemAnswer�ɓo�^����Ă���z�X�gID����� |
| graphid      | �K�{�B�g���t�B�b�N�擾�Ώۂ̃O���tID�BSystemAnswer�ɓo�^����Ă���z�X�g��IF���ƂɊ��蓖�Ă���O���tID����� |
| bandwidth    | �K�{�B�g���t�B�b�N�擾�Ώۂ̑ш�B�O���t�`�掞�̏c������l�Ɏg�p |
| description  | �C�ӁB�g���t�B�b�N�擾�Ώۂ̒��߁B���{�ꖼ�Ȃ� |

�f�[�^�擾
---------------

�R�}���h���C����艺�L�̏����Ńc�[�������s���Ă��������B
`[START_DATE]`��`[END_DATE]`�́AYYYY/MM/DD�`���Ŏ擾�J�n���Ǝ擾�I�������w�肵�Ă��������B

```sh
$ python main.py -h
usage: main.py [-h] --start_date [START_DATE] --end_date [END_DATE]

get SystemAnswer graph download as csv and png

optional arguments:
  -h, --help            show this help message and exit
  --start_date [START_DATE]
                        specify a start date of data. Style: YYYY/MM/DD
  --end_date [END_DATE]
                        specify a end date of data. Style: YYYY/MM/DD
```

�o�͌���
---------------

outputs�t�H���_�ɏo�̓t�@�C�����u����܂��B

�����
---------------

�c�[���̎��s�ɂ����艺�L�̃C���X�g�[�����K�v�ł�

* Python3
* Selenium
* Chromedriver
