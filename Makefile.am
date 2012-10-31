SUBDIRS = src ui 

bin_SCRIPTS = light-desktop-item-edit
CLEANFILES = $(bin_SCRIPTS)
EXTRA_DIST = light-desktop-item-edit.in

do_substitution = sed -e 's,[@]pythondir[@],$(pythondir),g' \
	-e 's,[@]PACKAGE[@],$(PACKAGE),g' \
	-e 's,[@]VERSION[@],$(VERSION),g' \
	-e 's,[@]pkgdatadir[@],$(pkgdatadir),g'	\
	-e 's,[@]pythondir[@],$(pythondir),g'	\
	-e 's,[@]PYTHON[@],$(PYTHON),g'	

light-desktop-item-edit: light-desktop-item-edit.in Makefile
	$(do_substitution) < $(srcdir)/light-desktop-item-edit.in > light-desktop-item-edit
	chmod +x light-desktop-item-edit


uninstall-local:
	-rm -r $(light_desktop_item_editdocdir)

