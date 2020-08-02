# Solution of the compressibility Z-Factor

The Z-factor does not depend on the magnitude of pressure and temperature, but on their values relative to critical pressure and temperature or reduced pressure and temperature.

In order to get the pseudo-critical temperature and pressure of the composition, we need to get as input: 

![Image of formula](https://github.com/FoxyChmoxy/z-factor/blob/master/docs/Screenshot%20from%202020-08-02%2015-40-57.png?raw=true)

- `n`   = the number of components in the composition
- `yi`  = number of moles of a particular component j
- `Tcj` = critical temperature of component j
- `pcj` = critical pressure of component j

We can use natural gas composition as an example:

![Image of example](https://github.com/FoxyChmoxy/z-factor/blob/master/docs/Screenshot%20from%202020-08-01%2012-55-34.png?raw=true)

From this table we can find out that:
- `n` = 5
- `P_pc` = `sum(yi * pcj)` = 826.92
- `T_pc` = `sum(yi * Tcj)` = 433.81

![Image of pseudo-critical values](https://github.com/FoxyChmoxy/z-factor/blob/master/docs/Screenshot%20from%202020-08-02%2015-51-16.png?raw=true)

```python
def get_data_from_file(filename):
    with open(filename, 'r') as file:
        array = file.read().splitlines()
        return [list(map(float, item.split())) for item in array]

def get_system_data_from_file(filename):
    with open(filename, 'r') as file:
        return tuple(map(float, file.readline().split()))

def get_pseudo_critical_temperature(data):
    T_c = 0
    for row in data:
        y_i, t_ci = row[0], row[1]
        T_c += y_i * t_ci
    return T_c

def get_pseudo_critical_pressure(data):
    P_c = 0
    for row in data:
        y_i, p_ci = row[0], row[2]
        P_c += y_i * p_ci
    return P_c

if __name__ == "__main__":
    input_file, system_file = sys.argv[1], sys.argv[2]

    data = get_data_from_file(input_file)
    T_system, P_system = get_system_data_from_file(system_file)
    
    T_c = get_pseudo_critical_temperature(data)
    P_c = get_pseudo_critical_pressure(data)
```

Now we need to calculate pseudo reduced value:
```python
def get_pseudo_reduced_value(system_value, critical_value):
    return system_value / critical_value

if __name__ == "__main__":
    P_pr = get_pseudo_reduced_value(P_system, P_c)
    T_pr = get_pseudo_reduced_value(T_system, T_c)
```
Then we can find out our Z-Factor with:

![Image of Z-Factor value](https://github.com/FoxyChmoxy/z-factor/blob/master/docs/photo_2020-08-02_15-46-03.jpg?raw=true)
```python
def get_z_factor(T_pr, P_pr):
    A = 1.39 * ((T_pr - 0.92) ** 0.5) - (0.36*T_pr) - 0.10
    E = 9*(T_pr - 1)
    B = (0.62 - 0.23*T_pr)*P_pr + ((0.066 / (T_pr - 0.86)) - 0.037)*(P_pr**2) + (0.32*(P_pr**2)) / 10*E
    C = 0.132 - 0.32 * math.log(T_pr)
    F = 0.3106 - 0.49*T_pr + 0.1824*(T_pr**2)
    D = 10 ** F

    return A + ((1 - A) / math.exp(B)) + (C * (P_pr ** D))
    
if __name__ == "__main__":
    z = get_z_factor(T_pr, P_pr)
```

# Web Interface

The web interface for users looks quite acceptable: with instructions on how to use it and instant results on an asynchronous request.

![Image of interface](https://github.com/FoxyChmoxy/z-factor/blob/master/docs/Screenshot%20from%202020-08-02%2015-28-46.png?raw=true)

index.html
```js
$.ajax({
    url: "/zfactor",
    type: "POST",
    data: $("form").serialize(),
    datatype: "json",
    success: function(response) {
        console.log(response);
        $("#result").html(`<h2>Z = ${response.result}</h2>`)
    }
});
```

routes.py
```python
@app.route('/zfactor', methods=['POST'])
def zfactor():
    molars = list(map(float, request.form['molars'].split()))
    temperatures = list(map(float, request.form['temperatures'].split()))
    pressures = list(map(float, request.form['pressures'].split()))

    data = [[molars[i], temperatures[i], pressures[i]] for i in range(len(molars))]

    T_system = float(request.form['tSystem'])
    P_system = float(request.form['pSystem'])

    T_c = get_pseudo_critical_temperature(data)
    P_c = get_pseudo_critical_pressure(data)

    P_pr = get_pseudo_reduced_value(P_system, P_c)
    T_pr = get_pseudo_reduced_value(T_system, T_c)

    z = get_z_factor(T_pr, P_pr)

    return jsonify({"result" : str(z.real) })
```

# Contribution

Despite the full implementation, the web interface still needs some work. In particular, there is a lack of data editing at the stage of adding and removing unnecessary records. The project is completely open to contribution, you can fork and make pull requests if you want to contribute.
