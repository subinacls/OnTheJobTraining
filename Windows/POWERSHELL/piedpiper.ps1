
function piedpipper() {
	$wmiLog = "Microsoft-Windows-WMI-Activity/Trace"
	echo y | Wevtutil.exe sl $wmiLog /e:true
	Read-Host -Prompt "Tracing WMI Started. Press [ENTER] to stop"
	echo y | Wevtutil.exe sl $wmiLog /e:false
	$events = Get-WinEvent -LogName $wmiLog -Oldest | Where-Object {$_.message.Contains("Operation = Start") -or $_.message.Contains("Operation = Provider") }
	 
	if ($events -eq $null)
	{
		Write-Host "No WMI events in trace!"
		return
	}
	 
	$table = New-Object System.Data.DataTable
	[void]$table.Columns.Add("Computer")
	[void]$table.Columns.Add("Namespace")
	[void]$table.Columns.Add("Type")
	[void]$table.Columns.Add("Query")
	[void]$table.Columns.Add("UserName")
	[void]$table.Columns.Add("Process")
	 
	ForEach ($event in $events)
	{
		switch ($event.Properties.Count)
		{
			6 {
				$typeStart = $event.Properties[1].Value.IndexOf("::")+2
				$typeEnd = $event.Properties[1].Value.IndexOf(" ",$typeStart) 
				$type = $event.Properties[1].Value.Substring($typestart,$typeEnd-$typeStart)
				$query = $event.Properties[1].Value.Substring($event.Properties[1].Value.IndexOf(":",$typeEnd)+2)
				$process = Get-Process -Id ($event.Properties[2].Value) -ErrorAction SilentlyContinue
				if ($process -eq $null) 
				{ 
					$process = "($($event.Properties[2].Value))"
				}
				else
				{
					$process = "$($process.Name) ($($process.Id))"
				}      
				foreach ($pipe in [System.IO.Directory]::GetFiles("\\.\pipe")) {
					[void]$table.Rows.Add(`
						$env:COMPUTERNAME,`
						"$pipe",`
						$type,`
						$query,`
						"N/A",
						$process)
				}
			}
			8 {
				$typeStart = $event.Properties[3].Value.IndexOf("::")+2
				$typeEnd = $event.Properties[3].Value.IndexOf(" ",$typeStart) 
				$type = $event.Properties[3].Value.Substring($typestart,$typeEnd-$typeStart)
				$query = $event.Properties[3].Value.Substring($event.Properties[3].Value.IndexOf(":",$typeEnd)+2)
				$process = Get-Process -Id ($event.Properties[6].Value) -ErrorAction SilentlyContinue
				if ($process -eq $null) 
				{ 
					$process = "($($event.Properties[6].Value))"
				}
				else
				{
					$process = "$($process.Name) ($($process.Id))"
				}
	 
				[void]$table.Rows.Add(`
					$event.Properties[4].Value,`
					$event.Properties[7].Value,`
					$type,`
					$query,`
					$event.Properties[5].Value,
					$process)
			}
			default
			{
				Write-Error "Unexpected number of event properties."
				Write-Host $event
				Write-Host $event.Properties
			}
		}
	}
	 
	$table | Out-GridView
}

