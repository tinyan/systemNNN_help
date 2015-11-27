#!/usr/mesh/bin/perl5

print "Content-type: text/html\n\n";

srand(time);

open (STDERR, ">&STDOUT");


$len=$ENV{'CONTENT_LENGTH'};
read (STDIN,$buf,$len);

@args = split(/&/, $buf);
foreach $arg (@args)
{
	($name, $val) = split (/=/, $arg);
	$val =~ s/\+/ /g;
	$val =~ s/%([0-9a-f][0-9a-f])/pack('C',hex($1))/egi;
	$field{$name} = $val;
}

$codedNumber = $field{'passcode'};

open (INFILE,"mada.htm");
while (<INFILE>)
{
	$tmp = $_;
	if ($tmp eq "<!--hidden->\n")
	{
		print "<INPUT NAME=\"passcode\" TYPE=hidden VALUE=\"" . $codedNumber ."\">";
	}
	else
	{
		print $tmp;
	}
}
close INFILE;


