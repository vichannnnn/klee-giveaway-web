# klee-giveaway-web

Development domain: dev.himaaa.xyz

Development bot: Yuna


# Endpoints

/login - redirects to authenticate


## after login (need login first to access, access stored in kuuki):

/user - get user info 
/guilds/guild_id - get all guild roles
/guilds/guild_id/role_id - get all role members

## example

input
```http://dev.himaaa.xyz/guilds/660135595250810881/798882908269051906```
output
```python
{
"624251187277070357": [
"Mira",
"7777"
],
"344350545697439747": [
"♡ 𝓴𝓪𝓷𝓪𝓮 ♡",
"3543"
]
}
```
