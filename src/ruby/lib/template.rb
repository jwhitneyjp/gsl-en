require 'qam/headerbody'

class Template

    def self.parse_file(path)
	hb = QAM::HeaderBody.parse_text_file(path)
	new(hb.body)
    end

    def initialize(template_text)
	@template_text = template_text
    end

    attr_reader :template_text

    class SubstitutionData
    	def initialize(title, pagetitle, css, javascript, banner_image, parent_breadcrumbs_html, content)
	    @title, @pagetitle, @css, @javascript, @banner_image, @parent_breadcrumbs_html, @content =
		title, pagetitle, css, javascript, base, banner_image, parent_breadcrumbs_html, content
	end
	attr_accessor :title, :pagetitle, :css, :javascript, :banner_image, :parent_breadcrumbs_html, :content
    end

    def render_html(substitution_data = SubstitutionData.new(nil, '', nil, '', ''))
	template_text.
	    gsub('@@title@@', substitution_data.pagetitle).
	    gsub('@@css@@', substitution_data.css).
	    gsub('@@javascript@@', substitution_data.javascript).
	    gsub('@@page-title@@', substitution_data.pagetitle).
	    gsub('@@banner-image@@', substitution_data.banner_image).
	    gsub('@@breadcrumbs@@', substitution_data.parent_breadcrumbs_html).
	    gsub('@@content@@',
		substitution_data.content_html)
    end

end
