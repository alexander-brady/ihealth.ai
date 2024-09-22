import Chat from './chat';
import { getUserOrRedirect } from '@propelauth/nextjs/server/app-router';

const Home = async () => {
  // If the user is not logged in, they will be redirected to the login page
   await getUserOrRedirect()

  return <Chat />
}
export default Home
