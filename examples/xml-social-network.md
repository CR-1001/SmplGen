<?xml version="1.0" encoding="UTF-8"?>
<socialNetwork>
    <users>
{%- for u in range(5) %}
        <user>
            <id>{{1000 + u}}</id>
            <username>{{user()}}</username>
            <firstName>{{first_name()}}</firstName>
            <lastName>{{first_name()}}</lastName>
            <email>{{email()}}</email>
            <birthdate>{{day()}}</birthdate>
            <friends>
            {%- for f in range(igauss(8,5)) %}
                <friend>{{1000 + iuniform(0,100)}}</friend>
            {%- endfor %}
            </friends>
        </user>
{%- endfor %}
    </users>
</socialNetwork>