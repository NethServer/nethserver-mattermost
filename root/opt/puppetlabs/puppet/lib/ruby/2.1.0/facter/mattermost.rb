# mattermost.rb

require 'rubygems'

Facter.add('mattermost') do
    setcode do
        mattermost = {}
        pass = File.read("/var/lib/nethserver/secrets/mattermost").strip

        posts = Facter::Core::Execution.exec("psql 'postgresql://mattuser:#{pass}@localhost:55432/mattermost' -Aqt -c 'SELECT count(*) FROM Posts WHERE DeleteAt = 0'")
        mattermost['posts'] = posts.to_i
        users = Facter::Core::Execution.exec("psql 'postgresql://mattuser:#{pass}@localhost:55432/mattermost' -Aqt -c 'SELECT count(*) FROM Users WHERE DeleteAt = 0'")
        mattermost['users'] = users.to_i
        teams = Facter::Core::Execution.exec("psql 'postgresql://mattuser:#{pass}@localhost:55432/mattermost' -Aqt -c 'SELECT count(*) FROM Teams WHERE DeleteAt = 0'")
        mattermost['teams'] = teams.to_i

        mattermost
    end
end
