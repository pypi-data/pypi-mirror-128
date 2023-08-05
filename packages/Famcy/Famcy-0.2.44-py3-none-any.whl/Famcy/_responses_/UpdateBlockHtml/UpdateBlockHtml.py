import Famcy

class UpdateBlockHtml(Famcy.FamcyResponse):
	"""
	This is the response to update a specific
	part of the famcy widget
	"""
	def __init__(self, extra_script=None, target=None):
		super(UpdateBlockHtml, self).__init__(target=target)
		self.extra_script = extra_script

	def response(self, sijax_response):
		body_html = self.target.render_inner()
		sijax_response.html('#'+self.target.id, self.target.body.html)
		sijax_response.script(self.extra_script)
		sijax_response.script(self.finish_loading_script)