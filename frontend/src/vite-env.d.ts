/// <reference types="svelte" />
/// <reference types="vite/client" />

type User = {
    "id": string,
    "username": string,
    "avatar": string,
    "avatar_decoration": string | null,
    "discriminator": string,
    "public_flags": number,
    "flags": number,
    "banner": string,
    "banner_color": string | null,
    "accent_color": string | null,
    "locale": string,
    "mfa_enabled": boolean,
    "premium_type": number,
    "guilds": {[key: string]: string}
}

type RoleList = {[key: string]: string}

type MemberList = {[key: string]: string[]}