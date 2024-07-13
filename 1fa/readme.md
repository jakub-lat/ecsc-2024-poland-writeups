# [1FA](https://hack.cert.pl/challenge/1fa)

## Task

We get access to a kubica fanklub website. We have the admin credentials `admin:RobertR@c!ng#24` and we have to bypass OTP.

## Research

In this suspicious code fragment:

```py
@app.route('/mfa', methods=['GET', 'POST'])
def mfa():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    if request.method == 'GET':
        mfa_login = session.get('mfa_login', None)
        if mfa_login is None:
            return redirect(url_for('login'))

        session['mfa_user'] = User.query.filter_by(login=mfa_login).first()
        if session['mfa_user'] is None:
            return redirect(url_for('login'))

        return render_template('mfa.html')

    mfa_user = session.get('mfa_user', None)
    totp = pyotp.TOTP(mfa_user.mfa_secret)
    if totp.verify(request.form.get('mfa_code')):
        login_user(session.get('user', None))
        return redirect(url_for('root'))

    return render_template('mfa.html', message='MFA verification failed!', type='warning')
```

Two different session variables are used - `user` and `mfa_user`.

To bypass the OTP, we need to craft a solve path where `user` is an attacker-controlled user with known OTP, and `mfa_user` is the admin account.


```py

@app.route('/mfa', methods=['GET', 'POST'])
def mfa():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    if request.method == 'GET':
        mfa_login = session.get('mfa_login', None)
        if mfa_login is None:
            return redirect(url_for('login'))

        session['mfa_user'] = User.query.filter_by(login=mfa_login).first()
        if session['mfa_user'] is None:
            return redirect(url_for('login'))

        return render_template('mfa.html')

    mfa_user = session.get('mfa_user', None)
    totp = pyotp.TOTP(mfa_user.mfa_secret)
    if totp.verify(request.form.get('mfa_code')):
        login_user(session.get('user', None))
        return redirect(url_for('root'))

    return render_template('mfa.html', message='MFA verification failed!', type='warning')
```

Here, the `mfa_user` is only assigned if we GET `/mfa` - if we only do POST `/mfa`, the `mfa_user` session variable can be something else, which leads to undefined behaviour.

## Solution

1. Register a user and set up MFA
2. Try to login as the just-registered user, without entering MFA
3. GET /mfa, so session.mfa_user will be set to our controlled user
4. Try to login as Kubica, so session.user will be admin
5. POST /mfa with the OTP of controlled user.
6. Profit


[Semi-automatic solve script](./solve.py)

`ecsc24{y0u'v3_w0n_7h3_r4c3}`