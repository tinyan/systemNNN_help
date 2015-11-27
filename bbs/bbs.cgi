#!/usr/local/bin/perl5

##print "Content-type: text/html\n\n";

require ('jcode.pl');

&dmycheck();

$len=$ENV{'CONTENT_LENGTH'};
if (($len == 0) || ($len eq ""))
{
##	print "LENGTH=".$len."\n";
	sleep(2);
	$len=$ENV{'CONTENT_LENGTH'};
}
read (STDIN,$buf,$len);

$cookies = $ENV{'HTTP_COOKIE'};
@pairs = split(/;/,$cookies);
foreach $pair (@pairs) {
   ($name, $value) = split(/\=/, $pair);
   $name =~ s/ //g;
   $cook{$name} = $value;
}

@args = split(/&/, $buf);
foreach $arg (@args)
{
	($name, $val) = split (/=/, $arg);
	$val =~ s/\+/ /g;
	$val =~ s/%([0-9a-f][0-9a-f])/pack('C',hex($1))/egi;
	$field{$name} = $val;
}

$password=$cook{'password'};

if ($field{"username"} ne "")
{
	$password=$field{"username"};
}

#$password =~ s/\</＜/g;
#$password =~ s/\>/＞/g;
$password =~ s/\"/”/g;
#$password =~ s/\'/’/g;
#$password =~ s/\;/；/g;
#$password =~ s/\,/、/g;
$password =~ s/ //g;
$password =~ s/\n//g;



print "Content-type: text/html\n";
if (($password ne "") && ($field{"bbscommand"} eq "write6"))
{
	print "Set-cookie: password=" . $password . ";expires=Fri, 31-Dec-2012 23:59:59 GMT\n";
}
print "\n";


##print "pass=" . $password . "<BR>\n";
##print "cook=" . $cookies . "<BR>\n";


$BBSMAX=300;


#&FileLockOn($LOCKFILE);

$command = $field{'command'};
$passcode = $field{'passcode'};
if ($passcode ne "666")
{
	$field{'bbscommand'} = "reload";
}

&CommandRoutine();

#&FileLockOff($LOCKFILE);

####################################################

sub CommandRoutine
{
	if ($command eq "bbs") {&BbsRoutine();}
	#elsif ($command eq "") {}
	#elsif ($command eq "") {}
	#elsif ($command eq "") {}
	else
	{
		$field{'bbscommand'}="reload";
		$field{'bbslines'}=5;
		&BbsRoutine();
	}
	
}


####################################################
sub BbsRoutine
{
	if ($field{'bbscommand'} eq "start")
	{
		&PrintHtml("bbs.htm");
	}

	if ($field{'bbscommand'} eq "reload")
	{
		&PrintHtml("bbs.htm");
	}

	if ($field{'bbscommand'} eq "write6")
	{
		if ($field{"bbstext"} ne "")
		{
			open(INFILE, "data/lastnum.txt");
			$num=<INFILE>;
			close INFILE;
			$num++;
			$num %= $BBSMAX;
			open (OUTFILE, ">data/lastnum.txt");
			print OUTFILE $num;
			close OUTFILE;
			chmod (0766,"data/lastnum.txt");
	
			open (OUTFILE, ">data/" . $num . ".txt");
			$uname = $field{"username"};
			if ($uname eq "")
			{
##				$uname = $ENV{"HTTP_REFERER"};
				$uname = "のら猫";
			}
			print OUTFILE $uname . "\n";
			print OUTFILE time() . "\n";
			print OUTFILE $ENV{"HTTP_REFERER"} . "\n";
			print OUTFILE $ENV{"REMOTE_ADDR"} . "\n";
			print OUTFILE $field{'bbstext'} . "\n";
			close OUTFILE;
			chmod (0766,"data/" . $num.".txt");
		}

		&PrintHtml("bbs.htm");
	}
}


####################################################

sub PrintHtml
{
    my ($fileName) = @_;
    my ($tmp);
    my ($tmp2);

	open (INFILEHTML,$fileName);
	while (<INFILEHTML>)
	{
		$tmp = $_;
		if ($tmp eq "<!--hidden-->\n")
		{
#			&PrintPasscode();
#			&PrintAreaZahyo();
		}
		elsif ($tmp eq "<!--bbssellines-->\n")
		{
			&PrintBbsSelLines();
		}
		elsif ($tmp eq "<!--username-->\n")
		{
			&PrintUserName();
		}
#		elsif ($tmp eq "<!--sysopflag-->\n")
#		{
#			&PrintSysopFlag();
#		}
		elsif ($tmp eq "<!--bbsdata-->\n")
		{
			&PrintBbsData();
		}
		else
		{
			print $tmp;
		}
	}
	close INFILEHTML;
}





sub PrintBbsData
{
    my ($i);
    my ($imax) = $field{'bbslines'};
    my ($tmp);
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$ydat,$isdat);
	my ($tmp00) = "￥たいにゃん￥\n";
	my ($tmp01) = "￥たいにゃん￥";
	my ($sysoptinyan) = 0;
	
	
	$_ = $tmp00;
	&jcode'convert(*_, 'sjis');
	$tmp00 = $_;
	
	$_ = $tmp01;
	&jcode'convert(*_, 'sjis');
	$tmp01 = $_;
	
	if ($tmp01 eq $field{"username"})
	{
		$sysoptinyan = 1;
	}

	
	if ($imax>$BBSMAX) {$imax=$BBSMAX;}
	open (INFILE,"data/lastnum.txt");
    my ($num)= <INFILE>;
	close INFILE;
	for ($i=0;$i<$imax;$i++)
	{
		if (open (INFILE, "data/" . $num . ".txt"))
		{
			$tmp = <INFILE>;

			$_ = $tmp;
			&jcode'convert(*_, 'sjis');
			$tmp = $_;
			if ($tmp ne $tmp00)
			{
				print "<B>" . $tmp . "</B>しゃま wroteにゃ:";
			}
			else
			{
				print "<I>たいにゃん</I> wroteにゃ:";
			}

			$tmp = <INFILE>;
			($sec,$min,$hour,$mday,$mon,$year,$wday,$ydat,$isdat)=localtime($tmp);
			$mon++;
                        $year += 1900;

			print " $year-$mon-$mday $hour:$min:$sec";

			print "<BR>\n";

#http_ref
			$tmp = <INFILE>;
if ($sysoptinyan == 1)
{
			print "HTTP_REF : " . $tmp . "<BR>\n";
}
			
#remote_addr			
			$tmp = <INFILE>;
if ($sysoptinyan == 1)
{
			print "REMOTE-ADDR : " . $tmp . "<BR>\n";
}
			

			print "<BLOCKQUOTE>\n";

			while (<INFILE>)
			{
				&jcode'convert(*_, 'sjis');
				print $_;

				print "<BR>\n";
			}
			print "</BLOCKQUOTE>\n";

			close INFILE;
			print "<HR>";
		}

		$num--;
		if ($num<0) {$num=$BBSMAX-1;}
	}
}


sub PrintBbsSelLines
{
    my ($num) = $field{'bbslines'};
    my (@tbl) = (5,10,20,50,100,300);
    my ($i);

	for ($i=0;$i<6;$i++)
	{
		print "<OPTION VALUE=\"" . $tbl[$i] . "\"";
		if ($tbl[$i] == $num)
		{
			print " SELECTED"
		}
		print ">" . $tbl[$i] . "\n"
	}
}


sub PrintUserName
{
	print "<INPUT NAME=\"username\" TYPE=text VALUE=\"";
##	print $ENV{"HTTP_REFERER"};	
##	print "名前なし";
	print $password;
	print "\" SIZE=30>\n";
}


#####################################################################


sub FileLockOn
{

    my ($loop,$datafile) = (0,@_);

	if ($ENV{'TINYAN_DEBUG'} ne "debug")
	{
		until ( symlink ($datafile,"${datafile}.filelock")) #  データファイルと同じディレクトリにシンボリックファイル作成
		{
			print "Wait...\n";
			if ($loop > 10)
			{
				unlink("${datafile}.filelock") || &error('【致命的】ロックを解除できません');
				&error('ロック中です。ブラウザのBackで戻ってください。');  #  もし10回待って、なおロック中なら、何らかの事故があったと見てロックを強制解除する。
			}
			sleep(2);   #  2秒待ってみる
			$loop++;
		}
	}
}


sub FileLockOff
{
	if ($ENV{'TINYAN_DEBUG'} ne "debug")
	{
	    my ($datafile) = @_;
		unlink("${datafile}.filelock") || &error("【致命的】ロックを解除できません");
	}
}

sub error
{
    my ($errmsg) = @_;
	print "<H1>エラーです！！</H1>";
	print $errmsg,"<br><hr>\n";
	exit(1);
}

sub dmycheck
{
	$b=1;
}
