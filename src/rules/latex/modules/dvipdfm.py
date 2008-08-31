# This file is part of Rubber and thus covered by the GPL
# (c) Emmanuel Beffara, 2003--2006
"""
PDF generation through dvipdfm with Rubber.
"""

import sys
from os.path import *

import rubber
from rubber import _
from rubber import *
from rubber.depend import Node

class Dep (Node):
	def __init__ (self, doc, target, source):
		Node.__init__(self, doc.env.depends, [target], [source])
		self.doc = doc
		self.env = doc.env
		self.source = source
		self.target = target
		self.options = []

	def run (self):
		msg.progress(_("running dvipdfm on %s") % self.source)
		cmd = ["dvipdfm"]
		for opt in self.doc.vars["paper"].split():
			cmd.extend(["-p", opt])
		cmd.extend(self.options + ["-o", self.target, self.source])
		if self.env.execute(cmd, kpse=1):
			msg.error(_("dvipdfm failed on %s") % self.source)
			return False
		return True

class Module (rubber.rules.latex.Module):
	def __init__ (self, doc, dict):
		self.doc = doc
		if doc.env.final.products[0][-4:] != ".dvi":
			msg.error(_("I can't use dvipdfm when not producing a DVI"))
			sys.exit(2)
		dvi = doc.env.final.products[0]
		pdf = dvi[:-3] + "pdf"
		self.dep = Dep(doc, pdf, dvi, doc.env.final)
		doc.env.final = self.dep

	def do_options (self, *args):
		self.dep.options.extend(args)
