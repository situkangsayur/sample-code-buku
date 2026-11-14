{ Kode 4.3: repeat-until di Pascal (Algoritma 4.5 BanyakDigit). }
program BanyakDigit;
var
  n, d: integer;
begin
  n := 2026;
  d := 0;
  repeat
    n := n div 10;
    d := d + 1;
  until n = 0;
  writeln(d);   { 4 }
end.
