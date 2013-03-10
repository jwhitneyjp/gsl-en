puts("Building website.")
system("ruby Install -C -q")

system("./Frontend.sh")

WEB_SERVER_PORT = 8080
require 'webrick'
docroot = File.dirname(File.expand_path($0)) + '/release/docroot/'
quiet_logger = WEBrick::BasicLog.new($stderr, WEBrick::Log::FATAL)
begin
    server = WEBrick::HTTPServer.new(
	:BindAddress => '127.0.0.1',
	:Port => WEB_SERVER_PORT,
	:Logger => quiet_logger,
	:AccessLog => [[ quiet_logger, "" ], [ quiet_logger, "" ]],
	:DocumentRoot => docroot)
    server_thread = Thread.new { server.start }
    puts("Web server started on port #{WEB_SERVER_PORT}.")
rescue Errno::EADDRINUSE
    puts("Another web server is listening on port #{WEB_SERVER_PORT}.")
end

puts("Browse the web site on http://127.0.0.1:8080/")
puts("Press Ctrl-BREAK to quit.")
server_thread.join
