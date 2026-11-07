-- uji generik buatan sendiri: mengembalikan baris yang MELANGGAR; nol baris = lulus
{% test nominal_positif(model, column_name) %}
select * from {{ model }} where {{ column_name }} <= 0
{% endtest %}

{% test jumlah_cabang_minimal(model, minimal) %}
select tgl, count(distinct cabang_id) as n_cabang
from {{ model }}
group by tgl
having count(distinct cabang_id) < {{ minimal }}
{% endtest %}
