# Copyright 2006-2007 by Starling Software, K.K.
# This is part of QAM from http://www.starling-software.com.
# For license terms, see the LICENSE.QAM file included with this distribution.

require 'fileutils'

module QAM; class Install

    include FileUtils

    class InstallDirs

	include QAM::Dirs

	# We have this here, instead of in QAM.dirs, because things running
	# out of the release directory should never depend on things outside
	# of the release directory.
	BASEDIR = File.expand_path(QAM.dirs.release('..'))

	def base(*path_components)
	    File.join(BASEDIR, *path_components)
	end

	def build(*pcs)
	    base('build', *pcs)
	end

	def extsrc(*pcs)
	    base('extsrc', *pcs)
	end

    end

    def initialize
	@dirs = InstallDirs.new
    end

    attr_reader :dirs

    ARGV.each { |arg| $quiet = true if arg == '-q' }
    def quiet_puts(m)
	puts m unless $quiet
    end

    def self.i; @instance ||= QAM::Install.new; end
    def self.d; i.dirs; end

    def self.install_lib_and_bin
	i.install_tree(d.mine('lib'), d.rubylib_site, :matching => /\.rb$/) if
	    File.directory?(d.mine('lib'))
	i.install_tree(d.mine('bin'), d.bin) if File.directory?(d.mine('bin'))
    end

    def install_tree(source_dir, destination, options = {})
	raise "'#{source_dir}' is not a directory or does not exist" unless
	    File.directory?(source_dir)
	options[:message] ||=
	    "  --- Installing #{source_dir.gsub(%r"#{dirs.base}/",'')}"
	quiet_puts(options[:message]) unless options[:message] == :none
	mkdir_p(destination)
	Dir["#{source_dir}/**/*"].each { |source_file|
	    next if options[:matching] &&
		! options[:matching].match(source_file)
	    dest = destination + '/' + source_file.gsub(source_dir + '/', '')
	    destdir = File.dirname(dest)
	    mkdir_p(destdir) unless File.directory?(destdir)
	    if File.directory?(source_file)
		mkdir_p(dest) unless File.directory?(dest)
	    else
		install(source_file, dest) if
		    ! File.exists?(dest) ||
		    (File.mtime(source_file) > File.mtime(dest))
	    end
	}
    end

    def run_quiet_install(dir_or_file, options = {})
	options[:quiet] = true
	run_install(dir_or_file, options)
    end

    def run_install(dir_or_file, options = {})
	options[:message] ||= "----- Installing #{dir_or_file}"
	if !$quiet && options[:message] != :none
	    puts(options[:message].
		gsub(Install.new.dirs.base + '/', '').
		gsub(/\/Install$/, ''))
	end
	command = /^mswin/.match(Config::CONFIG['host_os']) ? 'ruby ' : ''
	command += dir_or_file +
	    (File.directory?(dir_or_file) ? '/Install' : '') +
	    (($quiet || options[:quiet]) ? ' -q' : '')
	run_or_fail(command)
	self
    end

    def run_or_fail(command)
	system(command) || fail("Can't run #{command}")
    end

end; end

