package main;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.TimeUnit;


public class Main {

	public static void main(String[] args) {
		long begin = System.currentTimeMillis();

		Thread t = new Thread(new Runnable() {
			public void run() {
				 Main.startRequests(1000);
			}
	   });
		
		Thread t1 = new Thread(new Runnable() {
	         public void run() {
	              Main.startRequests(333);
	         }
	    });  
		Thread t2 = new Thread(new Runnable() {
	         public void run() {
	              Main.startRequests(333);
	         }
	    }); 
		Thread t3 = new Thread(new Runnable() {
	         public void run() {
	              Main.startRequests(333);
	         }
		}); 

		t.start();

		try {
		    t.join();
		    long end = System.currentTimeMillis();
		    long dt = end - begin;
			System.out.println("Total time: " + dt);
	    } catch (Exception e) {
			  e.printStackTrace();
		}
		
		begin = System.currentTimeMillis();
		
	    t1.start();
	    t2.start();
		t3.start();
		
	    try {
		    t1.join();
		    t2.join();
		    t3.join();
		    long end = System.currentTimeMillis();
		    long dt = end - begin;
			System.out.println("Total time parallelly: " + dt);
	    } catch (Exception e) {
			  e.printStackTrace();
	    }
	}
	
	public static void startRequests(int numberOfRequests){
		HttpURLConnection connection = null;  
		  try {
			  long begin = System.currentTimeMillis();
			  for(int i = 0; i < numberOfRequests; i++){
				  URL url = new URL("URL");

				  connection = (HttpURLConnection)url.openConnection();

				  connection.setRequestMethod("GET");
				  connection.setRequestProperty("Accept", "application/json");
				  connection.setRequestProperty("Cookie", "token=;");
				  connection.setUseCaches(false);
		
				  //Get Response  
				  InputStream is = connection.getInputStream();
				  BufferedReader rd = new BufferedReader(new InputStreamReader(is));
				  String line;
				  while((line = rd.readLine()) != null){}
			  }
			  long end = System.currentTimeMillis();
			  long dt = end - begin;
			  System.out.println("Time in thread: " + dt);
		  } catch (Exception e) {
			  e.printStackTrace();
		  } finally {
			  if(connection != null) connection.disconnect();
		  }
	}
	

}
