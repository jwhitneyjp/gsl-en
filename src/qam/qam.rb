# Copyright 2006-2007 by Starling Software, K.K.
# This is part of QAM from http://www.starling-software.com.
# For license terms, see the LICENSE.QAM file included with this distribution.

require 'rbconfig'

module QAM

    module Dirs

	def release(*path_components)
	    @release_dir ||= File.expand_path(__FILE__ + '/..')
	    File.join(@release_dir, *path_components)
	end

	def bin(*pcs)
	    release('bin', *pcs)
	end

	def rubylib(*pcs)
	    release('lib', 'ruby', Config::CONFIG['ruby_version'], *pcs)
	end

	def rubylib_arch(*pcs)
	    rubylib(Config::CONFIG['sitearch'], *pcs)
	end

	def rubylib_site(*pcs)
	    release('lib', 'ruby', 'site_ruby',
		Config::CONFIG['ruby_version'], *pcs)
	end

	def rubylib_sitearch(*pcs)
	    rubylib_site(Config::CONFIG['sitearch'], *pcs)
	end

	def find_mine
	    match_root = ($0[0,1] == '/')
	    match_root = ($0[0,3].match(%r'[A-Z]:/')) if QAM.platform(:win)
	    match_root ?
		File.expand_path($0 + '/..') :
		File.expand_path(Dir::pwd + '/' + $0 + '/..')
	end

	def mine(*pcs)
	    @mine ||= find_mine
	    File.join(@mine, *pcs)
	end

    end

    class DirsImplementation; include Dirs; end
    DIRS = DirsImplementation.new
    def self.dirs; DIRS; end

    def self.platform(platform)
	os = Config::CONFIG['target_os']
	case platform
	when :mac:	os.match(/^darwin/)
	when :win:	os.match(/^mswin/)
	else raise("Unknown platform: #{platform}")
	end
    end

    def self.error(message)
	$stderr.puts("ERROR: " + message)
	exit 1
    end

end

d = QAM.dirs
$LOAD_PATH.unshift(d.rubylib_sitearch)
$LOAD_PATH.unshift(d.rubylib_site)
$LOAD_PATH.unshift(d.rubylib_arch)
$LOAD_PATH.unshift(d.rubylib)
ENV['PATH'] = d.release('bin') + ':' + ENV['PATH']

begin
    require 'qam/ruby_extensions'
rescue LoadError
    # We've not installed QAM (yet).
end

require 'qam/install'
