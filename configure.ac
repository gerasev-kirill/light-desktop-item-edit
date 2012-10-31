AC_INIT([light-desktop-item-edit],[0.3])

AM_INIT_AUTOMAKE([1.10])

AM_SILENT_RULES([yes])

#with python3 program crashes on "import gi.repository"
PYTHON=/usr/bin/python2.7

AM_PATH_PYTHON(2.7)



GETTEXT_PACKAGE=light-desktop-item-edit
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE", [Gettext package])
AM_GLIB_GNU_GETTEXT
IT_PROG_INTLTOOL([0.40.0])


AC_CONFIG_FILES([ po/Makefile.in
Makefile
src/Makefile
ui/Makefile

])
AC_OUTPUT
