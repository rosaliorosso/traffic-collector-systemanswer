@echo off
REM �t�@�C�����s�t�H���_�ֈړ�
cd /d "%~dp0"

REM �f�[�^�擾���̐���
FOR /F "usebackq" %%a IN (`powershell "("Get-Date")".AddDays"("-1")".ToString"("'yyyy/MM/dd'")"`) DO SET targetdate=%%a

REM �f�[�^�擾
echo python main.py --start_date %targetdate% --end_date %targetdate%
python main.py --start_date %targetdate% --end_date %targetdate%
