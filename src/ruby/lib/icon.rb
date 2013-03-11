module Icon

    def self.uri_for(extension)
	@@icons ||= Dir[QAM::Install.new.dirs.base(
	    'src', 'docroot', 'docroot', 'icon', '*.png')].
	    collect { |path| File.basename(path, '.png') }
	name = @@icons.include?(extension) ? extension : 'unknown'
	return "/en/icon/#{name}.png"
    end

end
