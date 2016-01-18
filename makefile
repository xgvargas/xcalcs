#--------------------------------------------------------------------------
#
#    Makefile for PySide
#
#--------------------------------------------------------------------------


# UIC = c:\Python27\scripts\pyside-uic
# RCC = c:\Python27\Lib\site-packages\PySide\pyside-rcc
# LUP = c:\Python27\Lib\site-packages\PySide\lupdate
# LRL = c:\Python27\Lib\site-packages\PySide\lrelease

UIC = $(VIRTUAL_ENV)\Scripts\pyside-uic
RCC = $(VIRTUAL_ENV)\Lib\site-packages\PySide\pyside-rcc -py3
LUP = $(VIRTUAL_ENV)\Lib\site-packages\PySide\pyside-lupdate
LRL = $(VIRTUAL_ENV)\Lib\site-packages\PySide\lrelease

NIX = $(ProgramFilesX86)\git\bin


#--------------------------------------------------------------------------
VPATH = ui/

UI_FILES = $(patsubst ui/%.ui, %_ui.py, $(wildcard ui/*.ui))

RESOURCE_FILES = $(patsubst ui/%.qrc, %_rc.py, $(wildcard ui/*.qrc))

IMAGE_FILES = $(patsubst ui/%.svg, ui/%.extracted, $(wildcard ui/*.svg))

TRANSLATION_FILES = $(patsubst i18n/%.ts, i18n/%.qm, $(wildcard i18n/*.ts))

default: compile

compile: $(UI_FILES) $(RESOURCE_FILES) $(TRANSLATION_FILES)

.SECONDARY: $(IMAGE_FILES)

%.extracted : %.svg
	$(NIX)\bash.exe d:\bin\svg-extract.sh -f -o ui -s $@ $<

%_rc.py : %.qrc $(IMAGE_FILES)
	$(RCC) -o $@ $<

%_ui.py : %.ui
	$(UIC) -o $@ $<

%.qm : %.ts
	$(LRL) $< -qm $@

clean:
	del *_ui.py
	del *_rc.py
	del *.pyc
	-rd /s /q __pycache__
	-$(NIX)\cat ui/*.extracted | $(NIX)\xargs $(NIX)\rm.exe
	del ui\*.extracted
	del i18n\*.qm

.PHONY: images dist update

images: $(IMAGE_FILES)

dist:
# versao usando o Esky
	-rd /s /q dist
	python setup-esky.py bdist_esky
	"c:\Program Files\7-Zip\7z.exe" x -odist\pack dist\*.zip
	"$(ProgramFilesX86)\Inno Setup 5\ISCC.exe" setup.iss

# versao do cx-freeze
# .............

update:
	$(LUP) -verbose -noobsolete $(wildcard i18n/*.pro)
