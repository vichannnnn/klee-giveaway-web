/// <reference types="svelte" />
/// <reference types="vite/client" />

type User = {
    avatar: string,
    banner: string,
    discriminator: string,
    guilds: {[key: string]: string}
    id: string,
    username: string
}