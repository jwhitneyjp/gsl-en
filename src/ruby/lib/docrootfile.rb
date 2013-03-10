require 'qam/headerbody'

class DocrootFile

    def initialize(parent, header)
	@parent, @header = parent, header
    end

    def hidden; false; end

    attr_reader :parent
    attr_reader :header
    def 	dest_file;	raise("override me!"); end
    def 	content_html;	raise("override me!"); end


    def install_html(template)
    # HACK: for configurable sorting in folder contents box
    #if !header['link']
    mydest_file = dest_file.gsub(/\/[0-9][0-9]-(T-)*/, '/')
	File.open(mydest_file, 'w') { |s| s.write(template.render_html(self)) }
	children.each { |child| child.install_html(template) }
    end
    #end

    def inspect
	"[#{self.class.name}]"
    end

end
