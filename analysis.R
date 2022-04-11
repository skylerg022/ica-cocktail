
# Load libraries
library(tidyverse)
library(ica)
library(tuneR)

# Plot saving parameters
pic_width <- 9/2
pic_height <- 5
pic_units <- 'in'

# Set working directory if using RStudio
if (rstudioapi::isAvailable()) {
  setwd(dirname(rstudioapi::getSourceEditorContext()$path))
}

# Set seed
set.seed(293)

files <- list.files('data') %>%
  str_subset('.*CH7.*')
n_files <- length(files)

# Get samplerate, bits, and sample size
audio <- readWave(paste0('data/', files[1]))
samplerate <- audio@samp.rate
bit <- audio@bit
n <- length(audio@left)

X <- sapply(files, function(file) readWave(paste0('data/', file))@left)

# Create visual of data (4 mics)
X[,1:4] %>%
  as.data.frame() %>%
  set_names(paste0('V', 1:4)) %>%
  mutate(time = 1:n) %>%
  pivot_longer(cols = V1:V4,
               names_to = 'mic', values_to = 'value') %>%
  mutate(mic = mic %>%
           str_replace('V', 'Microphone ')) %>%
  ggplot(aes(time, value)) +
  geom_line() +
  facet_wrap(~ mic, ncol = 1) +
  theme_minimal() +
  labs(x = 'Time', y = 'Value')
ggsave('plots/ica_observed.png',
       width = pic_width,
       height = pic_height,
       units = pic_units,
       bg = 'white')


# Continue with ICA
n_comp <- 4
ica <- icafast(X[,1:4], nc = n_comp, fun = 'logcosh')
S <- ica$S %>%
  as.data.frame() %>%
  mutate(time = 1:n) %>%
  pivot_longer(cols = V1:V4,
               names_to = 'component', values_to = 'value') %>%
  mutate(component = component %>%
           str_replace('V', 'Component '))

S %>%
  ggplot(aes(time, value)) +
  geom_line() +
  facet_wrap(~ component, ncol = 1) +
  theme_minimal() +
  labs(x = 'Time', y = 'Value')

ggsave('plots/ica_results.png',
       width = pic_width,
       height = pic_height,
       units = pic_units,
       bg = 'white')

# Prep to save
sapply(1:n_comp,
       function(i) {
         new_audio <- Wave(left = ica$S[,i], samp.rate = samplerate, bit = bit) %>%
           normalize(as.character(bits))
         writeWave(new_audio, paste0('data/r_out', i, '.wav'))
         return()
       })




# Create visual for intended separation -----------------------------------

files <- list.files('data') %>%
  str_subset('.*P[0-9]{2}.*')

# Get samplerate, bits, and sample size
audio <- readWave(paste0('data/', files[1]))
samplerate <- audio@samp.rate
bit <- audio@bit
n <- length(audio@left)

voices <- sapply(files, function(file) readWave(paste0('data/', file))@left) %>%
  as.data.frame() %>%
  set_names(paste0('V', 1:4)) %>%
  mutate(time = 1:n) %>%
  pivot_longer(cols = V1:V4,
               names_to = 'speaker', values_to = 'value') %>%
  mutate(speaker = speaker %>%
           str_replace('V', 'Voice '))
voices %>%
  ggplot(aes(time, value)) +
  geom_line() +
  facet_wrap(~ speaker, ncol = 1) +
  theme_minimal() +
  labs(x = 'Time', y = 'Value')

ggsave('plots/goal_voices.png',
       width = pic_width,
       height = pic_height,
       units = pic_units,
       bg = 'white')
