# Stage 1: Build stage
FROM public.ecr.aws/lambda/python:3.11 as builder

WORKDIR /var/task
ENV USE_CUDA=0

# Copy function code
COPY src ${LAMBDA_TASK_ROOT}
COPY models ${LAMBDA_TASK_ROOT}/whisper
COPY bin /opt/bin
RUN chmod a+x /opt/bin/ffmpeg

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt
RUN pip freeze | grep nvidia > nvidia.txt
RUN pip uninstall -y torch
RUN pip uninstall -y -r nvidia.txt
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu


# Stage 2: Final stage
FROM public.ecr.aws/lambda/python:3.11

WORKDIR /var/task
ENV USE_CUDA=0
COPY --from=builder /var/task /var/task
COPY --from=builder /opt/bin/ /opt/bin/
COPY --from=builder /var/lang/lib/python3.11/site-packages /var/lang/lib/python3.11/site-packages


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.lambda_handler" ]


