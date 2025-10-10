# KickShopping Frontend

## Descripción
Frontend desarrollado con Next.js y TypeScript para la tienda KickShopping. Permite registro, login, gestión de productos, carrito y roles de usuario (vendedor/comprador).

## Requisitos
- Node.js 18 o superior
- npm

## Instalación
1. Clona el repositorio y navega a la carpeta `Frontend`.
2. Instala las dependencias:
   ```powershell
   npm install
   ```

## Configuración
- El archivo `next.config.ts` ya está preparado para desarrollo local.
- El frontend se conecta al backend en `http://localhost:8000`.
- No requiere configuración adicional para desarrollo local.

## Ejecución
1. Inicia el servidor de desarrollo:
   ```powershell
   npm run dev
   ```
2. Accede a la app en [http://localhost:3000](http://localhost:3000)

## Funcionalidades principales
- Registro de usuario como vendedor o comprador
- Login y autenticación con JWT
- Visualización y publicación de productos
- Carrito de compras
- Perfil de usuario con tipo (vendedor/comprador)
- Menús dinámicos según el rol

## Conexión con el backend
- El frontend realiza peticiones a la API FastAPI en `http://localhost:8000`.
- El token JWT se guarda en `localStorage` y se envía en las peticiones protegidas.

## Notas
- Si el backend no está corriendo, el frontend mostrará errores de conexión.
- Para que los roles funcionen correctamente, asegúrate de registrar usuarios con el rol deseado.

---

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).
# Frontend - KickShopping

Este proyecto es una aplicación web desarrollada con Next.js para la tienda KickShopping. Incluye páginas de productos, carrito, login, registro y perfil de usuario.

## Tecnologías principales
- [Next.js](https://nextjs.org/)
- [React](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [CSS Modules](https://nextjs.org/docs/pages/building-your-application/styling/css-modules)

## Estructura del proyecto

```
├── app/
│   ├── carrito/
│   ├── login/
│   ├── product/
│   ├── register/
│   ├── usuario/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── public/
│   └── (imágenes y recursos estáticos)
├── package.json
├── tsconfig.json
├── next.config.ts
└── README.md
```

## Instalación

1. Clona el repositorio:
	```powershell
	git clone https://github.com/kickshopping/Frontend.git
	```
2. Instala las dependencias:
	```powershell
	cd Frontend; npm install
	```

## Ejecución en desarrollo

```powershell
npm run dev
```
La aplicación estará disponible en `http://localhost:3000`.

## Scripts útiles
- `npm run dev`: Ejecuta el servidor de desarrollo
- `npm run build`: Compila la aplicación para producción
- `npm run start`: Inicia la aplicación en modo producción

## Contribuir
Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.

## Licencia
Este proyecto está bajo la licencia MIT.
## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
