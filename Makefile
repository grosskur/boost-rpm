# Makefile for source rpm: boost
# $Id$
NAME := boost
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
