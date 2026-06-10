# Computer Vision Reading Group @ RPL, KTH

This website is written using the [Vue.js](https://vuejs.org/) framework

## Project setup

- Clone this repo with `git clone https://github.com/rom42pla/kth_rpl_cv_reading_group.git`
- Install [Node.js](https://nodejs.org/en/download)
- Install the dependencies with `npm install`

## Compile and Hot-Reload for Development

```bash
npm run dev
```

The hot-reload preview is available at [http://localhost:5173](http://localhost:5173), but the port might change depending on your setup

## Deploy to the web

```sh
npm run deploy
```

The website will be available at [https://rom42pla.github.io/kth_rpl_cv_reading_group](https://rom42pla.github.io/kth_rpl_cv_reading_group)

## Repo structure

Nearly every code related to the website can be found in `src`

- Individual pages are found in `src` (e.g. `Home.vue`, `FAQs.vue`)
- Components that are reused throughout the website are found in `src/components` (e.g. `Navbar.vue`, `OrganizerCard.vue`)
- `main.ts` contains both links related to the routing in the webpage and common imports

Every file that can be accessed publicly (e.g. the favicon, the logos, the slides) can be found in `public`
