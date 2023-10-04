# web_modelo_booleano
![image](https://github.com/3rickDJ/web_modelo_booleano/assets/94492584/538474cc-1210-4389-98ce-969040da7699)

# Requirements
install Requirements

```bash
pip install --requirement requirements.txt
```
# Start Application

```bash
python app.py
```
Then browse to your localhost:5000
![image](https://github.com/3rickDJ/web_modelo_booleano/assets/94492584/c4a40041-f75c-4d64-bf74-391de137ff7d)


>> Note: The current path is located in the static folder as root `static/`

# Change the corpus
To change the corpus you need to specify the path and click `submit`
![image](https://github.com/3rickDJ/web_modelo_booleano/assets/94492584/f0820e42-cec4-4907-81f6-3b7d03004b43)

# Boolean search
## GUI
![image](https://github.com/3rickDJ/web_modelo_booleano/assets/94492584/7b8ecd3d-23e7-4c08-905f-f6bb22354e1e)

If your query has items to show they will be showed as a unordered list. Otherwise no documents will be shown.
## Constraints

Use only capital letters
The available operators are `!` as Not, `u` for union, `n` as intersection. Use `()` to group terms.

### Examples

`PERRO u GATO`
`!(PERRO u GATO)`
`(!(PERRO) n (CAMIÓN u COLADO))`
`(PERRO)`

