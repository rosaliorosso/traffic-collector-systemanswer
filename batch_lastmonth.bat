@echo off
REM �t�@�C�����s�t�H���_�ֈړ�
cd /d "%~dp0"

REM �f�[�^�擾���̐���
FOR /F "usebackq" %%a IN (`powershell "("Get-Date -Day 1")".AddMonths"("-1")".ToString"("'yyyy/MM/dd'")"`) DO SET targetdate1=%%a
FOR /F "usebackq" %%a IN (`powershell "("Get-Date -Day 1")".AddDays"("-1")".ToString"("'yyyy/MM/dd'")"`) DO SET targetdate2=%%a

REM �f�[�^�擾
echo python main.py --start_date %targetdate1% --end_date %targetdate2%
python main.py --start_date %targetdate1% --end_date %targetdate2%
