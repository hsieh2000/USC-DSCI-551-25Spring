/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class SQL2MR {

// NC-17, 85, Trailers;Commentaries, 2.99

  public static class TokenizerMapper 
       extends Mapper<Object, Text, Text, IntWritable>{
    
    private Text outputKey = new Text();
    private IntWritable outputValue = new IntWritable();
      
    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
	     // fill in code
       String[] toks = value.toString().split(",");

       String special_features = toks[toks.length - 1];
       String rating = toks[toks.length - 2];
       float rental_rate = Float.parseFloat(toks[toks.length - 5]);
       int _length = Integer.parseInt(toks[toks.length - 4]);

       if ((special_features.contains("Trailer")) && (rental_rate >= 2)) {

        System.out.println("special features: " + special_features);
        System.out.println("rental_rate : " + rental_rate);
        System.out.println("length : " + _length + "\n");

        outputKey.set(rating);
        outputValue.set(_length);
        context.write(outputKey, outputValue);
       }
	  }
  }
  
  public static class MyReducer 
       extends Reducer<Text,IntWritable,Text,FloatWritable> {
    private FloatWritable result = new FloatWritable();

    public void reduce(Text key, Iterable<IntWritable> values, 
                       Context context
                       ) throws IOException, InterruptedException {
      // fill in code
      float sum = 0, cnt = 0;
      for (IntWritable val: values) {
        int v = val.get();
        sum += v;
        cnt++;
      }

      if (cnt > 60) {
        float avg = sum/cnt;
        System.out.println("avg = " + sum + "/" + cnt + " = " + avg + "\n");

        result.set(avg);
        context.write(key, result);  
      }   
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
    if (otherArgs.length < 2) {
      System.err.println("Usage: sql2mr <in> [<in>...] <out>");
      System.exit(2);
    }
    Job job = Job.getInstance(conf, "sql2mr");
    job.setJarByClass(SQL2MR.class);
    job.setMapperClass(TokenizerMapper.class);
    //job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(MyReducer.class);
    job.setMapOutputKeyClass(Text.class);
    job.setMapOutputValueClass(IntWritable.class);
    
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(FloatWritable.class);
    
    for (int i = 0; i < otherArgs.length - 1; ++i) {
      FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
    }
    FileOutputFormat.setOutputPath(job,
      new Path(otherArgs[otherArgs.length - 1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
