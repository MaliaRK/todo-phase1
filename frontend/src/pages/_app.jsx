import '../styles/globals.css';
import { NotificationProvider } from '../components/Notification';
import { TasksProvider } from '../contexts/TasksContext';
import { AuthProvider } from '../auth/auth_provider';

function MyApp({ Component, pageProps }) {
  return (
    <AuthProvider>
      <NotificationProvider>
        <TasksProvider>
          <Component {...pageProps} />
        </TasksProvider>
      </NotificationProvider>
    </AuthProvider>
  );
}

export default MyApp;