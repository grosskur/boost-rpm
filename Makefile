# Makefile for source rpm: boost
# $Id: Makefile,v 1.1 2004/09/09 03:35:58 cvsdist Exp $
NAME := boost
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
